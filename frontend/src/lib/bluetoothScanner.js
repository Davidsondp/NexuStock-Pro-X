export const connectBluetoothScanner = async () => {
  try {
    const device = await navigator.bluetooth.requestDevice({
      acceptAllDevices: true,
      optionalServices: ['generic_access']
    });
    
    const server = await device.gatt.connect();
    const service = await server.getPrimaryService('generic_access');
    const characteristic = await service.getCharacteristic('device_name');
    
    return {
      device,
      onData: callback => {
        characteristic.addEventListener(
          'characteristicvaluechanged', 
          event => callback(event.target.value)
        );
        characteristic.startNotifications();
      }
    };
  } catch (error) {
    console.error('Error Bluetooth:', error);
    throw error;
  }
};
