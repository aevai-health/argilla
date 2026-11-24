<template>
  <div class="title-area --body1" :aria-label="question.title">
    <span
      class="suggestion-info"
      v-text="question.title"
      v-required-field="{
        show: question.isRequired || question.name.endsWith('_comment'),
        color: '#cf3832',
      }"
    />
    <!-- aevai: show the description under the title instead of behind an info tooltip -->
    <p
      v-if="question.description"
      class="question-description --body2"
      v-text="question.description"
    />
  </div>
</template>

<script>
export default {
  name: "QuestionHeader",
  props: {
    question: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
.question-description {
  margin: 0.4em 0 0;
  color: var(--fg-secondary);
  font-weight: 400;
  white-space: pre-line; // keep the blank line between explanation and scale
}

.title-area {
  color: var(--fg-primary);
  font-weight: 500;
  &__suggestion-icon {
    cursor: default;
    fill: var(--bg-opacity-54);
  }
}

.icon {
  color: var(--fg-tertiary);
}

.info-icon {
  display: flex;
  flex-basis: 37px;
}

span {
  word-break: break-word;
  line-height: 1.2em;
}

.icon-info {
  display: inline-flex;
  width: 20px;
  height: 20px;
  margin: 0;
  padding: 0;
  vertical-align: middle;
  &[data-title] {
    position: relative;
    overflow: visible;
    &:before,
    &:after {
      margin-top: 0;
    }
  }
}
</style>
