<template>
    <v-container>
        <v-row align="baseline">
            <div>
                <span>Current Room: </span>
                <span>{{ currentRoomId }}</span>
            </div>
            <v-text-field label="Room-ID" v-model="joinRoom.roomId"/>
            <v-btn @click="onJoinRoom">Join Room</v-btn>
        </v-row>
    </v-container>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import 'vue-class-component/hooks';

@Component({})
export default class SyncControl extends Vue {
    joinRoom = {
        roomId: '',
    }

    onJoinRoom() {
        this.$store.dispatch('joinRoom', this.joinRoom.roomId);
    }

    get currentRoomId() {
        return this.$store.state.rooms.roomId;
    }
}
</script>

<style scoped lang="scss">

</style>
