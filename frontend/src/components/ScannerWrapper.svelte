<script>
  import { isMobile, hasCamera } from '../utils/device';
  import MobileScanner from './MobileScanner.svelte';
  import DesktopScanner from './DesktopScanner.svelte';
  
  let mobileMode = false;
  let hasCameraSupport = false;
  
  onMount(async () => {
    mobileMode = isMobile();
    hasCameraSupport = await hasCamera();
  });
</script>

{#if !hasCameraSupport}
  <div class="alert">
    <p>Se requiere acceso a la cámara para escanear códigos</p>
    <a href="/manual-entry" class="btn">Entrada Manual</a>
  </div>
{:else if mobileMode}
  <MobileScanner />
{:else}
  <DesktopScanner />
{/if}
