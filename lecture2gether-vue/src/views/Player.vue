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

    require('videojs-contrib-hls/dist/videojs-contrib-hls.js')
    export default {
        data() {
            return {
                playerOptions: {
                    // videojs options
                    muted: true,
                    language: 'en',
                    playbackRates: [0.7, 1.0, 1.3, 1.5, 2.0],
                    sources: [{
                        withCredentials: false,
                        type: "application/x-mpegURL",
                        src: "https://fms2.rrz.uni-hamburg.de/vod/_definst/smil:8l2gbap2029/65-301_video-27959_2020-04-24_22-33.smil/playlist.m3u8"
                    }],
                    html5: { hls: { withCredentials: false }},
                    poster: "/static/images/author.jpg",
                }
            }
        },
        mounted() {
            console.log('this is current player instance object', this.player)
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
