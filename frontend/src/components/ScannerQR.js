import { Html5QrcodeScanner } from 'html5-qrcode';

export class ProductScanner {
  constructor(elementId, onScan) {
    this.scanner = new Html5QrcodeScanner(
      elementId,
      {
        fps: 10,
        qrbox: { width: 250, height: 250 },
        formatsToSupport: [
          Html5QrcodeSupportedFormats.UPC_A,
          Html5QrcodeSupportedFormats.EAN_13
        ]
      },
      false
    );
    this.onScan = onScan;
  }

  start() {
    this.scanner.render((decodedText) => {
      this.onScan(decodedText);
      this.stop();
    }, (error) => {
      console.error("Error al escanear:", error);
    });
  }

  stop() {
    this.scanner.clear();
  }
}

// Uso en componente React/Svelte/Vue:
// const scanner = new ProductScanner('qr-reader', (code) => {
//   console.log('Código escaneado:', code);
// });
// scanner.start();
