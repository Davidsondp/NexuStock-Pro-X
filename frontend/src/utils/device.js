export const isMobile = () => {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent
  );
};

export const isIOS = () => {
  return /iPhone|iPad|iPod/i.test(navigator.userAgent);
};

export const isAndroid = () => {
  return /Android/i.test(navigator.userAgent);
};

export const hasCamera = async () => {
  if (!navigator.mediaDevices?.enumerateDevices) return false;
  
  try {
    const devices = await navigator.mediaDevices.enumerateDevices();
    return devices.some(device => device.kind === 'videoinput');
  } catch {
    return false;
  }
};
