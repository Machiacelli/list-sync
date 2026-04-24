<template>
  <Card class="glass-card border border-purple-500/30 hover:border-purple-400/50 transition-all duration-300">
    <div class="space-y-4">

      <!-- Header -->
      <div class="flex items-center gap-2.5">
        <div class="p-2 rounded-lg bg-gradient-to-br from-purple-600/20 to-purple-500/10 border border-purple-500/30">
          <KeyIcon class="w-4 h-4 text-purple-400" />
        </div>
        <div class="flex-1">
          <h3 class="text-base font-bold titillium-web-semibold">
            Trakt API Configuration (Optional)
          </h3>
          <p class="text-[10px] text-muted-foreground font-medium">
            Optional integration for external list sources (IMDb mode works without it)
          </p>
        </div>
      </div>

      <!-- Form Fields -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

        <!-- Trakt Client ID (OPTIONAL) -->
        <div class="md:col-span-2">
          <label class="block text-xs font-semibold mb-2 text-foreground">
            Trakt Client ID
            <span class="text-muted-foreground ml-1 text-xs">(optional)</span>
          </label>

          <Input
            v-model="localValue.clientId"
            type="text"
            placeholder="Optional: enter Trakt Client ID"
            :icon="KeyIcon"
            @update:model-value="emitUpdate"
          />

          <p class="text-xs text-muted-foreground mt-1.5">
            Only needed if you use Trakt lists. IMDb-only mode ignores this.
          </p>
        </div>

        <!-- Limit -->
        <div>
          <label class="block text-xs font-semibold mb-2 text-foreground">
            Special Lists Items Limit
          </label>

          <Input
            v-model.number="localValue.specialItemsLimit"
            type="number"
            :min="1"
            :max="100"
            placeholder="20"
            :icon="HashIcon"
            @update:model-value="emitUpdate"
          />

          <p class="text-xs text-muted-foreground mt-1.5">
            Number of items fetched (only applies if Trakt is used)
          </p>
        </div>

      </div>

      <!-- Help Section -->
      <div class="border-t border-purple-500/20 pt-4">

        <button
          type="button"
          class="flex items-center justify-between w-full text-left group"
          @click="showHelp = !showHelp"
        >
          <div class="flex items-center gap-2">
            <HelpCircleIcon class="w-4 h-4 text-purple-400" />
            <span class="text-sm font-semibold text-purple-400">
              {{ showHelp ? 'Hide' : 'Show' }} Help
            </span>
          </div>

          <ChevronDownIcon
            class="w-4 h-4 text-purple-400 transition-transform duration-200"
            :class="{ 'rotate-180': showHelp }"
          />
        </button>

        <div v-if="showHelp" class="mt-4 space-y-3">

          <div class="bg-info/10 border border-info/20 rounded-lg p-3">
            <div class="flex items-start gap-2">
              <InfoIcon class="w-4 h-4 text-info flex-shrink-0 mt-0.5" />
              <div class="text-xs">
                <p class="font-semibold text-info mb-1">What is this?</p>
                <ul class="text-muted-foreground space-y-0.5 list-disc list-inside">
                  <li>Trakt is optional for external list providers</li>
                  <li>IMDb-only mode works without any configuration</li>
                  <li>Used only for enhanced metadata resolution (optional)</li>
                </ul>
              </div>
            </div>
          </div>

        </div>
      </div>

    </div>
  </Card>
</template>

<script setup lang="ts">
import {
  Key as KeyIcon,
  Info as InfoIcon,
  HelpCircle as HelpCircleIcon,
  Hash as HashIcon,
  ChevronDown as ChevronDownIcon,
} from 'lucide-vue-next'

interface TraktApiSettings {
  clientId: string
  specialItemsLimit: number
}

interface Props {
  modelValue: TraktApiSettings
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:modelValue': [value: TraktApiSettings]
}>()

const localValue = ref({ ...props.modelValue })
const showHelp = ref(false)

watch(
  () => props.modelValue,
  (newValue) => {
    localValue.value = { ...newValue }
  },
  { deep: true }
)

const emitUpdate = () => {
  emit('update:modelValue', { ...localValue.value })
}
</script>
