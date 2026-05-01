// ============================================================
// ble-shim.js — minimal runtime so js/ble.js can run standalone
// (outside index.html) on pages like docs/joystick-lab.html.
//
// js/ble.js was written for the main app. It relies on globals
// that core.js + lang.js + others define (btDevice, writeChar,
// addLogLine, setConnectionStatus, t, UART_SERVICE_UUID, etc.)
// and on a handful of DOM elements (#connectBtn, #deviceName, …).
//
// This shim provides bare minimum stubs so ble.js works unchanged.
// Pages embedding ble.js can override window.RobiBle hooks to
// redirect logs / status / RX into their own UI.
//
// MUST load BEFORE js/ble.js.
// ============================================================
(function () {
  'use strict';

  // ---- 1. UART service UUID (declared in core.js in main app) ----
  if (typeof window.UART_SERVICE_UUID === 'undefined') {
    window.UART_SERVICE_UUID = '6e400001-b5a3-f393-e0a9-e50e24dcca9e';
  }

  // ---- 2. State globals ble.js mutates ----
  // Use window.* because ble.js writes them at file scope.
  window.btDevice    = null;
  window.btServer    = null;
  window.uartService = null;
  window.notifyChar  = null;
  window.writeChar   = null;
  window.isConnected = false;

  // ---- 3. Hooks the host page can override ----
  // Default impls just log to console and call console-driven UI.
  window.RobiBle = window.RobiBle || {
    onLog:      (line, level) => { /* host overrides */ },
    onStatus:   (state, name) => { /* host overrides */ },
    onRxLine:   (line)        => { /* host overrides */ },
    onToast:    (msg, level)  => { /* host overrides */ },
  };

  // ---- 4. Stubs ble.js calls ----
  if (typeof window.addLogLine !== 'function') {
    window.addLogLine = (line, level) => window.RobiBle.onLog(line, level);
  }
  if (typeof window.setConnectionStatus !== 'function') {
    window.setConnectionStatus = (state) => {
      window.isConnected = !!state;
      window.RobiBle.onStatus(!!state, window.btDevice && window.btDevice.name);
    };
  }
  if (typeof window.t !== 'function') {
    // Tiny i18n stub — return a friendly fallback for known keys
    const dict = {
      log_web_bt_na:      'Web Bluetooth not available',
      log_requesting:     'Requesting device…',
      log_connecting:     'Connecting…',
      log_getting_uart:   'Fetching UART service…',
      log_getting_chars:  'Fetching characteristics…',
      log_connected:      'Connected.',
      log_reconnecting:   'Reconnecting…',
      log_reconnect_fail: 'Reconnect failed.',
      toast_reconnecting: 'Reconnecting',
    };
    window.t = (key) => dict[key] || key;
  }
  if (typeof window.showToast !== 'function') {
    window.showToast = (msg, level) => window.RobiBle.onToast(msg, level);
  }
  if (typeof window.handleUartLine !== 'function') {
    window.handleUartLine = (line) => window.RobiBle.onRxLine(line);
  }

  // ---- 5. DOM stubs — ble.js touches #connectBtn / #deviceName / etc. ----
  // If the host page doesn't provide these elements, create hidden
  // placeholders so ble.js's setProperty / textContent calls don't throw.
  const ensure = (id) => {
    let el = document.getElementById(id);
    if (!el) {
      el = document.createElement('div');
      el.id = id;
      el.style.display = 'none';
      // append on DOMContentLoaded (body might not exist yet)
      if (document.body) document.body.appendChild(el);
      else document.addEventListener('DOMContentLoaded', () => document.body.appendChild(el));
    }
    return el;
  };
  ['connectBtn', 'disconnectBtn', 'connectionStatus', 'deviceName',
   'serviceUuidDisplay', 'rxCharUuidDisplay', 'txCharUuidDisplay',
   'serialNumber'].forEach(ensure);
})();
