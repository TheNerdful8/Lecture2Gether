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

    import videojs from 'video.js'
    import Component from "vue-class-component";
    import Vue from "vue";
    import {Prop} from "vue-property-decorator";
    import VueTypes from "vue-types";

    window.videojs = videojs

    require('videojs-contrib-hls/dist/videojs-contrib-hls.js');
    require('videojs-youtube/dist/Youtube');

    @Component({})
    export default class L2gPlayer extends Vue {
        @Prop(VueTypes.string.isRequired)
        url!: string;

        get playerOptions() {
            let type = "";
            if (this.url.endsWith(".m3u8")) {
                type = "application/x-mpegURL";
            } else if (this.url.endsWith(".mp4")) {
                type = "video/mp4";
            } else {
                const url = new URL(this.url);
                if (["youtube.com", "www.youtube.com", "youtu.be"].includes(url.hostname)) {
                    type = "video/youtube";
                }
            }

            return {
                // videojs options
                muted: true,
                language: 'en',
                playbackRates: [0.7, 1.0, 1.3, 1.5, 2.0],
                sources: [{
                    type: type,
                    src: this.url,
                }],
                techOrder: ["youtube", "html5"],
                poster: "/static/images/author.jpg",
            }
        }

        get player() {
            return this.$refs.videoPlayer.player
        }

        // listen event
        onPlayerPlay(player) {
            console.log('send play')
        }

        onPlayerPause(player) {
            console.log('send pause')
        }

        // player is ready
        playerReadied(player) {
            console.log('send player ready')
            // player.[methods]
        }
    }
</script>

<style scoped lang="scss">
</style>
