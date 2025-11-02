<template>
  <div class="editor-container">
    <textarea
      v-model="content"
      @input="onInput"
      class="w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
      :placeholder="placeholder"
      :rows="rows"
    ></textarea>
  </div>
</template>

<script>
export default {
  name: 'Editor',
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: 'Enter content...'
    },
    rows: {
      type: Number,
      default: 5
    }
  },
  emits: ['update:modelValue'],
  data() {
    return {
      content: this.modelValue
    }
  },
  watch: {
    modelValue(newVal) {
      this.content = newVal
    }
  },
  methods: {
    onInput() {
      this.$emit('update:modelValue', this.content)
    }
  }
}
</script>