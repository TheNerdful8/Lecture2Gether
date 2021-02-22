<template>
    <div>
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
        <video-meta-data>
        </video-meta-data>
    </div>
</template>

<script lang="ts">
// eslint-disable-next-line import/no-extraneous-dependencies
import videojs from 'video.js';
import Component from 'vue-class-component';
import Vue from 'vue';
import { Watch } from 'vue-property-decorator';
import videoPlayer from 'vue-video-player/src/player.vue';
import { checkURL } from '@/mediaURLs';
import VideoMetaData from '@/components/VideoMetaData.vue';

// eslint-disable-next-line @typescript-eslint/ban-ts-ignore
// @ts-ignore
window.videojs = videojs;

require('videojs-contrib-hls/dist/videojs-contrib-hls.js');
require('videojs-youtube/dist/Youtube');

@Component({
    components: { videoPlayer, VideoMetaData },
})
export default class L2gPlayer extends Vue {
    // To avoid re-sending the received events to the other users, we set the following flags
    // They are set to true when the user interacts with the player and set to false when he receives his own state
    skipNextPauseSend = false;

    skipNextPlaySend = false;

    skipNextSecondsSend = false;

    skipNextPlaybackRateSend = false;

    skipNextVideoURLSend = false;

    // The first play and first seek happen when the big play button is pressed
    // We do not want to send these events
    firstPlay = true;

    firstSeek = true;

    // After the first seek, the player time is set to the current time in the video.
    // This calls the play/pause event again.
    playPauseAfterFirstSeek = false;

    get url() {
        return this.$store.state.player.videoUrl;
    }

    get playerOptions() {
        let source;
        let playbackRates;
        try {
            source = this.getSourceFromURL(this.url);
            playbackRates = this.getPlaybackRatesFromSource(source.type);
        } catch (e) {
            console.error(e);
            // Show error page
        }

        return {
            // videojs options
            muted: false,
            language: 'en',
            fluid: true,
            playbackRates,
            sources: [source],
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

    getPlaybackRatesFromSource(src: string): Number[] {
        if (src === 'video/youtube') {
            // YouTube does not support player speed above 2x
            return [0.75, 1.0, 1.25, 1.5, 1.75, 2.0];
        } else {
            return [0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5];
        }
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
        if (this.firstPlay) {
            // re-join room to re-receive current state
            // this is necessary to recalculate the time we should have reached in the video
            this.firstPlay = false;
            this.$store.dispatch('joinRoom', this.$store.state.rooms.roomId);
            return;
        }
        if (this.playPauseAfterFirstSeek) {
            // We now have the correct time and pause state and can set the player's pause state accordingly.
            // Then, we are ready to be a regular player and the setup is finished.
            //this.onPausedChange();
            this.playPauseAfterFirstSeek = false;
            return;
        }
        console.log("play event");
        if (this.$store.state.player.paused != false){
            this.$store.dispatch('setVideoState', {
                paused: false,
                seconds: 0,
                playbackRate: this.player.playbackRate(),
            });
        }
    }

    onPlayerPause() {
        if (this.playPauseAfterFirstSeek) {
            //this.onPausedChange();
            this.playPauseAfterFirstSeek = false;
            return;
        }
        console.log("pause event");
        if (this.$store.state.player.paused != true){
            this.$store.dispatch('setVideoState', {
                paused: true,
                seconds: 0,
                playbackRate: this.player.playbackRate(),
            });
        }
    }

    onPlayerSeeked() {
        if (this.firstSeek) {
            // firstSeek happens after the big play button was pressed.
            // Next, the response from asking for the current state will be received.
            // That triggers an update of onSecondsChange to set the player to the correct time.
            // Finally, we have to adjust the play state. That's what playPauseAfterFirstSeek is for.
            this.firstSeek = false;
            this.playPauseAfterFirstSeek = true;
            return;
        }
        if (this.skipNextSecondsSend) {
            this.skipNextSecondsSend = false;
            return;
        }
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
                return;
            }
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
        this.player.playbackRate(this.$store.state.player.playbackRate);
        if (this.$store.state.player.paused) {
            this.player.pause();
        } else {
            this.player.play();
        }
    }

    @Watch('$store.state.player.paused')
    async onPausedChange() {
        if (this.$store.state.player.paused) {
            this.player.pause();
        } else {
            this.player.play();
        }
    }

    @Watch('$store.state.player.seconds')
    async onSecondsChange() {
        if (this.$store.state.player.sender === this.$store.state.socketId) {
            this.skipNextSecondsSend = false;
            return;
        }
        if (Math.abs(this.player.currentTime() - this.$store.state.player.seconds) > 1) {
            this.skipNextSecondsSend = true;
            this.player.currentTime(this.$store.state.player.seconds);
        }
    }

    @Watch('$store.state.player.videoUrl')
    async onURLChange() {
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

<style lang="scss">
@import "~video.js/dist/video-js.css";
.video-js .vjs-volume-control {
    padding-right: 1em;
}
.video-js .vjs-time-control {
    padding: 0;
}
.video-js .vjs-current-time {
    display: block;
}
.video-js .vjs-time-divider {
    display: block;
    padding: 0;
    min-width: 1em;
}
.video-js .vjs-duration {
    display: block;
}
.vjs-menu-button-popup .vjs-menu .vjs-menu-content {
    max-height: 16em;
}
</style>
