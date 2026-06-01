import { ref, watch } from 'vue'

/**
 * Animates a number from 0 to `target` over `duration` ms using easeOutExpo.
 * Returns a reactive `display` ref you bind in the template.
 */
export function useCounter(targetRef, duration = 900, decimals = 0) {
  const display = ref(0)
  let raf = null

  function animate(target) {
    cancelAnimationFrame(raf)
    const start = display.value
    const delta = target - start
    if (delta === 0) return
    const t0 = performance.now()

    function step(now) {
      const elapsed = now - t0
      const progress = Math.min(elapsed / duration, 1)
      // easeOutExpo
      const ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress)
      display.value = parseFloat((start + delta * ease).toFixed(decimals))
      if (progress < 1) raf = requestAnimationFrame(step)
    }
    raf = requestAnimationFrame(step)
  }

  watch(targetRef, (val) => animate(Number(val) || 0), { immediate: true })

  return display
}
