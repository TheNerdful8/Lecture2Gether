<template>
    <v-app>
        <v-content>
            <router-view/>
        </v-content>
    </v-app>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

@Component({})
export default class L2gHome extends Vue {
    created(): void {
        this.$store.dispatch('fetchSettings');
    }
}
</script>

<style lang="scss">
    @use "src/styles/global_style";

    #app {
        font-family: Avenir, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
    }

    #nav {
        padding: 30px;

        a {
            font-weight: bold;
            color: #2c3e50;

            &.router-link-exact-active {
                color: #42b983;
            }
        }
    }
</style>
