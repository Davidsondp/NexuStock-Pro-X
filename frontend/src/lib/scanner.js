import { Html5QrcodeScanner } from 'html5-qrcode';

export const initScanner = (elementId, onSuccess, onError) => {
  const config = {
    fps: 15,
    qrbox: { width: 250, height: 250 },
    formatsToSupport: [
      Html5QrcodeSupportedFormats.UPC_A,
      Html5QrcodeSupportedFormats.EAN_13,
      Html5QrcodeSupportedFormats.CODE_128
    ],
    experimentalFeatures: {
      useBarCodeDetectorIfSupported: true
    }
  };

  const scanner = new Html5QrcodeScanner(elementId, config, false);
  
  scanner.render(
    decodedText => {
      scanner.clear();
      onSuccess(decodedText);
    },
    error => onError(error)
  );

  return scanner;
};
