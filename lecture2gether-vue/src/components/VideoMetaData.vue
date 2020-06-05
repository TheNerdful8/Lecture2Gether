<template>
    <div class="video-meta-data" style="visibility: hidden;">
        <div class="title">
            {{ videoMetaData.title }}
        </div>
        <a class="creator" :href="videoMetaData.creatorLink">
            {{ videoMetaData.creator }}
        </a>
        <div class="date">
            {{ videoDate }}
        </div>
        <a class="license" :href="videoMetaData.licenseLink">
            License: {{ videoMetaData.license }}
        </a>
    </div>
</template>

<script lang="ts">
// eslint-disable-next-line import/no-extraneous-dependencies
import Component from 'vue-class-component';
import Vue from 'vue';

@Component
export default class VideoMetaData extends Vue {
    get videoMetaData() {
        return this.$store.state.player.videoMetaData;
    }

    get videoDate() {
        const date = new Date(Date.parse(this.$store.state.player.videoMetaData.date));
        return date.toLocaleDateString();
    }
}
</script>

<style scoped lang="scss">
</style>
