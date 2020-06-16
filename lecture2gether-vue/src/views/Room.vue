<template>
    <div>
        <PasswordDialog v-if="this.$store.getters.authRequired" class="password-dialog"></PasswordDialog>
        <l2g-player v-if="!this.$store.getters.authRequired && this.$store.state.player.videoUrl" class="l2g-player"></l2g-player>
        <v-overlay :value="!roomExists" light>
            <v-card class="room-card pa-12">
                <h2 class="display-1 heading ">Room does not exist (anymore)!</h2>
                <router-link :to="{ name: 'home' }">
                    <v-btn class="new-button mt-12" color="secondary">Create new room</v-btn>
                </router-link>
            </v-card>
        </v-overlay>
    </div>
</template>

<script lang="ts">
// @ is an alias to /src
import Vue from 'vue';
import Component from 'vue-class-component';
import L2gPlayer from '@/components/Player.vue';
import { Watch } from 'vue-property-decorator';
import { AuthState } from '@/plugins/store/player';
import PasswordDialog from '@/components/PasswordDialog.vue';

@Component({
    components: { PasswordDialog, L2gPlayer },
})
export default class L2gPlayerView extends Vue {
    roomExists = true;

    @Watch('$route.params.roomId')
    async onRouteChange() {
        if (this.$store.state.isConnected) {
            await this.syncRoomId();
        }
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
