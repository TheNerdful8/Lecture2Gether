<template>
    <v-container fluid>
        <v-row align="center" justify="center">
            <v-col cols="4">
                <!--v-progress-circular indeterminate color="primary"/ -->
            </v-col>
        </v-row>
    </v-container>
</template>

<script lang="ts">
// @ is an alias to /src
import Vue from 'vue';
import Component from 'vue-class-component';
import { Watch } from 'vue-property-decorator';

@Component({
    components: {},
})
export default class L2gHome extends Vue {
    @Watch('$store.state.isConnected')
    async onConnectedChanged() {
        await this.$store.dispatch('newRoom');
        await this.$router.push({
            name: 'room',
            params: {
                roomId: this.$store.state.rooms.roomId,
            },
        });
    }
}
</script>

<style scoped lang="scss">
</style>
