<template>
    <v-app>
        <v-main>
            <Toolbar :collapsed="isCollapsed"></Toolbar>
            <router-view/>
        </v-main>
        <lecture2-gether-footer/>
    </v-app>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';
import { connect, disconnect } from '@/plugins/socket.io';
import Toolbar from '@/components/Toolbar.vue';
import Lecture2GetherFooter from '@/components/Lecture2GetherFooter.vue';

@Component({
    components: { Lecture2GetherFooter, Toolbar },
})
export default class App extends Vue {
    created(): void {
        connect(this.$store)
        window.addEventListener('beforeunload', this.onClose);
    }

    onClose(): void {
        this.$store.dispatch('leaveRoom').then(() => disconnect());
    }

    get isCollapsed(): boolean {
        return (this.$store.state.player.videoMetaData && this.$store.state.player.videoMetaData.url !== '') || this.$store.getters.authRequired;
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
