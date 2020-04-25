<template>
    <video-player class="video-player-box"
                  ref="videoPlayer"
                  :options="playerOptions"
                  :playsinline="true"

                  @play="onPlayerPlay"
                  @pause="onPlayerPause"
                  @ready="playerReadied">
    </video-player>
</template>

<script lang="ts">
// eslint-disable-next-line import/no-extraneous-dependencies
import videojs from 'video.js';
import Component from 'vue-class-component';
import Vue from 'vue';
import { Prop } from 'vue-property-decorator';
import VueTypes from 'vue-types';
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
        @Prop(VueTypes.string.isRequired) url!: string;

        get playerOptions() {
            let type = 'video/mp4';

            // First, try extension based file types
            const extension = this.url.split('.').pop();
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
            try {
                const url = new URL(this.url);
                switch (url.hostname) {
                case 'youtube.com':
                case 'www.youtube.com':
                case 'youtu.be':
                    type = 'video/youtube';
                    break;
                default:
                    throw new Error('URL not supported');
                }
            } catch (e) {
                // Show error page, the url was invalid
            }

            return {
                // videojs options
                muted: true,
                language: 'en',
                width: '750px',
                playbackRates: [0.7, 1.0, 1.3, 1.5, 2.0],
                sources: [{
                    type,
                    src: this.url,
                }],
                techOrder: ['youtube', 'html5'],
                poster: '/static/images/author.jpg',
            };
        }

        get player(): videojs.Player {
            // @ts-ignore
            return this.$refs.videoPlayer.player;
        }

        // listen event
        onPlayerPlay() {
            console.log('send play');
        }

        onPlayerPause() {
            console.log('send pause');
        }

        // player is ready
        playerReadied() {
            console.log('send player ready');
            // player.[methods]
        }
}
</script>

<style scoped lang="scss">
@import "~video.js/dist/video-js.css" ;
</style>
