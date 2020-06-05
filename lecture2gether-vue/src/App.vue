<template>
    <v-app>
        <v-content>
            <Toolbar :collapsed="isCollapsed"></Toolbar>
            <router-view/>
        </v-content>
    </v-app>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';
import { connect, disconnect } from '@/plugins/socket.io';
import Toolbar from '@/components/Toolbar.vue';

@Component({
    components: { Toolbar },
})
export default class App extends Vue {
    created(): void {
        this.$store.dispatch('fetchSettings')
            .then(() => {
                connect(this.$store);
            });
        window.addEventListener('beforeunload', this.onClose);
    }

    onClose(): void {
        this.$store.dispatch('leaveRoom').then(() => disconnect());
    }

    get isCollapsed(): boolean {
        return this.$store.state.player.videoUrl !== '' || this.$store.getters.authRequired;
    }
}
</script>

<style lang="scss">
    @use "src/styles/global_style";
    @import '~@mdi/font/css/materialdesignicons.css';
    @import '~typeface-roboto/index.css';

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
