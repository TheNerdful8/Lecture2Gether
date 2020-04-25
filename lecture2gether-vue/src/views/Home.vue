<template>
    <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
            <v-col cols="4">
                <v-progress-circular indeterminate color="primary"/>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
// @ is an alias to /src
import Vue from 'vue';
import Component from 'vue-class-component';

@Component({})
export default class L2gHome extends Vue {
    mounted() {
        this.$store.dispatch('newRoom').finally(console.log);
    }
}
</script>

<style scoped lang="scss">
</style>
