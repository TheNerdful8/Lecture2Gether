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

<script>

    import videojs from 'video.js'
    window.videojs = videojs

    require('videojs-contrib-hls/dist/videojs-contrib-hls.js');
    require('videojs-youtube/dist/Youtube');
    export default {
        data() {
            return {
                playerOptions: {
                    // videojs options
                    muted: true,
                    language: 'en',
                    playbackRates: [0.7, 1.0, 1.3, 1.5, 2.0],
                    sources: [{
                        type: "application/x-mpegURL",
                        src: "https://fms2.rrz.uni-hamburg.de/vod/_definst/smil:8l2gbap2029/65-301_video-27959_2020-04-24_22-33.smil/playlist.m3u8"
                        //type: "video/youtube",
                        //src: "https://www.youtube.com/watch?v=7y1xJAVZxXg",
                        //type: "video/mp4",
                        //src: "https://www.math.uni-hamburg.de/home/reiher/lehre/SoSe20/Graphentheorie1/Vorlesungen/Grth1-VL1.mp4"
                    }],
                    techOrder: ["youtube", "html5"],
                    poster: "/static/images/author.jpg",
                }
            }
        },
        mounted() {
        },
        computed: {
            player() {
                return this.$refs.videoPlayer.player
            }
        },
        methods: {
            // listen event
            onPlayerPlay(player) {
                console.log('send play')
            },
            onPlayerPause(player) {
                console.log('send pause')
            },
            // player is ready
            playerReadied(player) {
                console.log('send player ready')
                // player.[methods]
            }
        }
    }
</script>

<style scoped lang="scss">
</style>
