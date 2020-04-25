<template>
    <v-container class="fill-height" fluid>
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
    onConnectedChanged(): void {
        this.$store.dispatch('newRoom');
    }
}
</script>

<style scoped lang="scss">
</style>
