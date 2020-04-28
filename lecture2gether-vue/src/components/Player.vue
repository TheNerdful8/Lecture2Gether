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
    skipNextPauseSend = false;

    skipNextPlaySend = false;

    skipNextSecondsSend = false;

    skipNextPlaybackRateSend = false;

    skipNextVideoURLSend = false;

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
        if (this.skipNextPlaySend) {
            this.skipNextPlaySend = false;
            console.log('this.skipNextPlaySend = false');
            return;
        }
        console.log('pl');
        this.$store.dispatch('setVideoState', {
            paused: false,
            seconds: this.player.currentTime(),
            playbackRate: this.player.playbackRate(),
        });
    }

    onPlayerPause() {
        if (this.skipNextPauseSend) {
            this.skipNextPauseSend = false;
            console.log('this.skipNextPauseSend = false');
            return;
        }
        console.log('pa');
        this.$store.dispatch('setVideoState', {
            paused: true,
            seconds: this.player.currentTime(),
            playbackRate: this.player.playbackRate(),
        });
    }

    onPlayerSeeked() {
        if (this.skipNextSecondsSend) {
            this.skipNextSecondsSend = false;
            console.log('this.skipNextSecondsSend = false');
            return;
        }
        console.log('se');
        this.$store.dispatch('setVideoState', {
            paused: this.player.paused(),
            seconds: this.player.currentTime(),
            playbackRate: this.player.playbackRate(),
        });
    }

    onPlayerRate() {
        if (this.player.playbackRate() !== this.$store.state.player.playbackRate) {
            if (this.skipNextPlaybackRateSend) {
                this.skipNextPlaybackRateSend = false;
                console.log('this.skipNextPlaybackRateSend = false');
                return;
            }
            console.log('ra');
            this.$store.dispatch('setVideoState', {
                paused: this.player.paused(),
                seconds: this.player.currentTime(),
                playbackRate: this.player.playbackRate(),
            });
        }
    }

    mounted(): void {
        // Player was mounted, set state
        console.log('mounted', this.$store.state.player.seconds);
        this.player.src(this.getSourceFromURL(this.$store.state.player.videoUrl));
        this.player.currentTime(this.$store.state.player.seconds);
        this.player.playbackRate(this.$store.state.player.playbackRate);
        if (this.$store.state.player.paused) {
            this.player.pause();
        } else {
            this.player.play();
        }
    }

    @Watch('$store.state.player.paused')
    async onPausedChange() {
        console.log(this.$store.state.player.sender, this.$store.state.socketId);
        if (this.$store.state.player.sender === this.$store.state.socketId) {
            this.skipNextPauseSend = false;
            this.skipNextPlaySend = false;
            return;
        }
        if (this.$store.state.player.paused) {
            this.skipNextPauseSend = true;
            this.player.pause();
        } else {
            this.skipNextPlaySend = true;
            this.player.play();
        }
    }

    @Watch('$store.state.player.seconds')
    async onSecondsChange() {
        console.log('seconds change')
        if (this.$store.state.player.sender === this.$store.state.socketId) {
            this.skipNextSecondsSend = false;
            return;
        }
        if (Math.abs(this.player.currentTime() - this.$store.state.player.seconds) > 1) {
            this.skipNextSecondsSend = true;
            this.player.currentTime(this.$store.state.player.seconds);
        }
    }

    @Watch('$store.state.player.videoURL')
    async onURLChange() {
        if (this.$store.state.player.sender === this.$store.state.socketId) {
            this.skipNextVideoURLSend = false;
            return;
        }
        this.skipNextVideoURLSend = true;
        this.player.src(this.getSourceFromURL(this.$store.state.player.videoUrl));
    }

    @Watch('$store.state.player.playbackRate')
    async onPlayerRateChange() {
        if (this.$store.state.player.sender === this.$store.state.socketId) {
            this.skipNextPlaybackRateSend = false;
            return;
        }
        this.skipNextPlaybackRateSend = true;
        this.player.playbackRate(this.$store.state.player.playbackRate);
    }
}
</script>

<style scoped lang="scss">
@import "~video.js/dist/video-js.css" ;
</style>
