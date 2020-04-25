<template>
    <l2g-player url="https://www.youtube.com/watch?v=m8UQ4O7UiDs"></l2g-player>
</template>

<script lang="ts">
// @ is an alias to /src
import Vue from 'vue';
import Component from 'vue-class-component';
import L2gPlayer from '@/components/Player.vue';
import { Watch } from 'vue-property-decorator';

@Component({
    components: { L2gPlayer },
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
}
</script>

<style scoped lang="scss">
</style>
