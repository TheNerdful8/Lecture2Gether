<template>
    <v-app>
        <v-content>
            <Toolbar :collapsed="isCollapsed"></Toolbar>
            <router-view/>
        </v-content>
        <v-footer>
            <v-spacer></v-spacer>
            <img src="/img/icons/GitHub.svg" alt="GitHub logo" class="mr-2"/>
            <a href="https://github.com/TheNerdful8/Lecture2Gether" class="footer-link">Lecture2Gether on Github</a>
            <v-spacer></v-spacer>
        </v-footer>
    </v-app>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';
import { connect } from '@/plugins/socket.io';
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

    .footer-link {
        color: #222222!important;
    }

    .footer-link:link {
        text-decoration: none;
    }

    .footer-link:hover {
        text-decoration: underline;
    }
</style>
