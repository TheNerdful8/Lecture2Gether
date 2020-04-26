<template>
    <video-player class="video-player-box"
                  ref="videoPlayer"
                  :options="playerOptions"
                  :playsinline="true"

                  @play="onPlayerPlay"
                  @pause="onPlayerPause">
    </video-player>
</template>

<script lang="ts">
// eslint-disable-next-line import/no-extraneous-dependencies
import videojs from 'video.js';
import Component from 'vue-class-component';
import Vue from 'vue';
import { Watch } from 'vue-property-decorator';
import videoPlayer from 'vue-video-player/src/player.vue';

// eslint-disable-next-line @typescript-eslint/ban-ts-ignore
// @ts-ignore
window.videojs = videojs;

require('videojs-contrib-hls/dist/videojs-contrib-hls.js');
require('videojs-youtube/dist/Youtube');

@Component({
    components: { videoPlayer },
})
export default class L2gPlayer extends Vue {
    get url() {
        return this.$store.state.player.videoUrl;
    }

    get playerOptions() {
        const sources = [];
        try {
            sources.push(this.getSourceFromURL(this.url));
        } catch (e) {
            // Show error page
        }

        return {
            // videojs options
            muted: false,
            language: 'en',
            width: '750px',
            playbackRates: [0.7, 1.0, 1.3, 1.5, 2.0],
            sources,
            techOrder: ['youtube', 'html5'],
            poster: '/static/images/author.jpg',
        };
    }

    get player(): videojs.Player {
        // @ts-ignore
        return this.$refs.videoPlayer.player;
    }

    getSourceFromURL(url: string): {type: string; src: string} {
        let type = 'video/mp4';

        // First, try extension based file types
        const extension = url.split('.').pop();
        switch (extension) {
        case 'm3u8':
            type = 'application/x-mpegURL';
            break;
        case 'mp4':
            type = 'video/mp4';
            break;
        case 'ogg':
            type = 'video/ogg';
            break;
        case 'webm':
            type = 'video/webm';
            break;
        default:
            // Set a known type for an unknown url results in a useful error message
            type = 'video/mp4';
        }

        // Then, try hostname based types
        const parsedUrl = new URL(this.url);
        switch (parsedUrl.hostname) {
        case 'youtube.com':
        case 'www.youtube.com':
        case 'youtu.be':
            type = 'video/youtube';
            break;
        default:
            throw new Error('URL not supported');
        }
        return {
            type,
            src: url,
        };
    }

    onPlayerPlay() {
        this.$store.dispatch('setVideoState', {
            paused: false,
            seconds: this.player.currentTime(),
        });
    }

    onPlayerPause() {
        this.$store.dispatch('setVideoState', {
            paused: true,
            seconds: this.player.currentTime(),
        });
    }

    @Watch('$store.state.player.paused')
    async onPausedChange() {
        this.player.currentTime(this.$store.state.player.seconds);
        if (this.$store.state.player.paused) {
            this.player.pause();
        } else {
            this.player.play();
        }
    }

    @Watch('$store.state.player.videoURL')
    async onURLChange() {
        this.player.selectSource([this.getSourceFromURL(this.$store.state.player.videoUrl)]);
    }
}
</script>

<style scoped lang="scss">
@import "~video.js/dist/video-js.css" ;
</style>
