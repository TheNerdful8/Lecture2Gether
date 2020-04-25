<template>
    <l2g-player url="https://www.youtube.com/watch?v=m8UQ4O7UiDs"></l2g-player>
</template>

<script>
// @ is an alias to /src
import Vue from 'vue';
import Component from 'vue-class-component';
import L2gPlayer from '@/components/Player.vue';

@Component({ components: { L2gPlayer } })
export default class L2gPlayerView extends Vue {
}
</script>

<style scoped lang="scss">
</style>
