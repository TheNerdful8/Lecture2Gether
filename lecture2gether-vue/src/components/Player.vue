<template>
    <video-player class="video-player-box"
                  ref="videoPlayer"
                  :options="playerOptions"
                  :playsinline="true"
                  :events="['seeked', 'ratechange']"

                  @play="onPlayerPlay"
                  @pause="onPlayerPause"
                  @seeked="onPlayerSeeked"
                  @ratechange="onPlayerRate">
    </video-player>
</template>

<script lang="ts">
// eslint-disable-next-line import/no-extraneous-dependencies
import videojs from 'video.js';
import Component from 'vue-class-component';
import Vue from 'vue';
import { Watch } from 'vue-property-decorator';
import videoPlayer from 'vue-video-player/src/player.vue';
import { checkURL } from '@/mediaURLs';

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
            console.error(e);
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
            youtube: {
                ytControls: 0,
            },
        };
    }

    get player(): videojs.Player {
        // @ts-ignore
        return this.$refs.videoPlayer.player;
    }

    getSourceFromURL(url: string): {type: string; src: string} {
        // shared media logic in src/mediaURLs.ts checkURL
        const res = checkURL(url);
        if (res === undefined) {
            throw new Error('URL not supported');
        } else {
            return {
                type: res.type,
                src: res.src.toString(),
            };
        }
    }

    onPlayerPlay() {
        this.$store.dispatch('setVideoState', {
            paused: false,
            seconds: this.player.currentTime(),
            playbackRate: this.player.playbackRate(),
        });
    }

    onPlayerPause() {
        this.$store.dispatch('setVideoState', {
            paused: true,
            seconds: this.player.currentTime(),
            playbackRate: this.player.playbackRate(),
        });
    }

    onPlayerSeeked() {
        this.$store.dispatch('setVideoState', {
            paused: this.player.paused(),
            seconds: this.player.currentTime(),
            playbackRate: this.player.playbackRate(),
        });
    }

    onPlayerRate() {
        if (this.player.playbackRate() !== this.$store.state.player.playbackRate) {
            this.$store.dispatch('setVideoState', {
                paused: this.player.paused(),
                seconds: this.player.currentTime(),
                playbackRate: this.player.playbackRate(),
            });
        }
    }

    mounted(): void {
        // Player was mounted, set state
        this.player.src(this.getSourceFromURL(this.$store.state.player.videoUrl));
        this.player.currentTime(this.$store.state.player.seconds);
        if (this.$store.state.player.paused) {
            this.player.pause();
        } else {
            this.player.play();
        }
    }

    @Watch('$store.state.player.paused')
    async onPausedChange() {
        console.log(this.$store.state.player.sender, this.$store.state.socketId);
        if (this.$store.state.player.sender === this.$store.state.socketId) return;
        if (this.$store.state.player.paused) {
            this.player.pause();
        } else {
            this.player.play();
        }
    }

    @Watch('$store.state.player.seconds')
    async onSecondsChange() {
        if (this.$store.state.player.sender === this.$store.state.socketId) return;
        if (Math.abs(this.player.currentTime() - this.$store.state.player.seconds) > 1) {
            this.player.currentTime(this.$store.state.player.seconds);
        }
    }

    @Watch('$store.state.player.videoURL')
    async onURLChange() {
        if (this.$store.state.player.sender === this.$store.state.socketId) return;
        this.player.src(this.getSourceFromURL(this.$store.state.player.videoUrl));
    }

    @Watch('$store.state.player.playbackRate')
    async onPlayerRateChange() {
        if (this.$store.state.player.sender === this.$store.state.socketId) return;
        this.player.playbackRate(this.$store.state.player.playbackRate);
    }
}
</script>

<style scoped lang="scss">
@import "~video.js/dist/video-js.css" ;
</style>
