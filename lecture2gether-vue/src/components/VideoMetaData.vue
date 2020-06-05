<template>
    <div class="video-meta-data" style="visibility: hidden;">
        <div class="title">
            {{ videoMetaData.Title }}
        </div>
        <a class="creator" :href="videoMetaData.CreatorLink">
            {{ videoMetaData.Creator }}
        </a>
        <div class="date">
            {{ videoDate }}
        </div>
        <a class="license" :href="videoMetaData.LicenseLink">
            License: {{ videoMetaData.License }}
        </a>
    </div>
</template>

<script lang="ts">
// eslint-disable-next-line import/no-extraneous-dependencies
import Component from 'vue-class-component';
import Vue from 'vue';
import { Watch } from 'vue-property-decorator';

@Component({
    components: { VideoMetaData },
})
export default class VideoMetaData extends Vue {

    get videoMetaData() {
        return this.$store.state.player.videoMetaData;
    }

    get videoDate() {
        const date = new Date(Date.parse(this.$store.state.player.videoMetaData.Date));
        return date.toLocaleDateString();
    }
}
</script>

<style scoped lang="scss">
</style>
