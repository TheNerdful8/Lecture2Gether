<template>
    <div>
        <PasswordDialog v-if="authRequired" class="password-dialog"></PasswordDialog>
        <l2g-player v-if="!authRequired" class="l2g-player" url="https://www.youtube.com/watch?v=gkC6YEinomA"></l2g-player>
    </div>
</template>

<script lang="ts">
    // @ is an alias to /src
    import Vue from 'vue';
    import Component from 'vue-class-component';
    import L2gPlayer from '@/components/Player.vue';
    import {Watch} from 'vue-property-decorator';
    import {AuthState} from '@/plugins/store/player';
    import PasswordDialog from "@/components/PasswordDialog.vue";

    @Component({
    components: { PasswordDialog, L2gPlayer },
})
export default class L2gPlayerView extends Vue {
    async mounted() {
        if (this.$store.state.isConnected) {
            await this.syncRoomId();
        }
    }

    async updated() {
        await this.syncRoomId();
    }

    @Watch('$store.state.isConnected')
    async onConnectedChanged(value: boolean, oldValue: boolean) {
        if (!oldValue && value) {
            await this.syncRoomId();
        }
    }

    /**
     * Ensures that the room we are currently connected to (the one in the store) is the same as the url parameter.
     */
    async syncRoomId() {
        const isSynced = this.$store.state.rooms.roomId === this.$route.params.roomId;
        if (!isSynced) {
            await this.$store.dispatch('joinRoom', this.$route.params.roomId);
        }
    }

    get authRequired() {
        return this.authState === AuthState.NECESSARY
            || this.authState === AuthState.CHECKING
            || this.authState === AuthState.FAILURE;
    }

    get authState() {
        return this.$store.state.player.auth;
    }
}
</script>

<style scoped lang="scss">
    .l2g-player > * {
        width: 100%!important;
    }
    .l2g-player {
        margin: auto;
        //hacky way to force centered video.
        //this size has to be the same as the video
        //width in src/components/Player.vue
        max-width: 750px;
    }

    .password-dialog {
        margin: auto;
    }
</style>
