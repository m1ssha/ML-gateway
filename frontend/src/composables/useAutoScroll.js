import { ref, watch, nextTick, onMounted, onUnmounted } from 'vue'

export function useAutoScroll(trigger) {
  const containerRef = ref(null)
  const isUserScrolling = ref(false)

  const scrollToBottom = async (behavior = 'smooth') => {
    if (!containerRef.value) return
    
    await nextTick()
    containerRef.value.scrollTo({
      top: containerRef.value.scrollHeight,
      behavior
    })
  }

  const handleScroll = () => {
    if (!containerRef.value) return
    
    const { scrollTop, scrollHeight, clientHeight } = containerRef.value
    // If we are not at the bottom (with some threshold), user is scrolling up
    const isAtBottom = scrollHeight - scrollTop - clientHeight < 50
    isUserScrolling.value = !isAtBottom
  }

  watch(trigger, () => {
    if (!isUserScrolling.value) {
      scrollToBottom()
    }
  }, { deep: true })

  onMounted(() => {
    if (containerRef.value) {
      containerRef.value.addEventListener('scroll', handleScroll)
      scrollToBottom('auto')
    }
  })

  onUnmounted(() => {
    if (containerRef.value) {
      containerRef.value.removeEventListener('scroll', handleScroll)
    }
  })

  return {
    containerRef,
    scrollToBottom
  }
}
