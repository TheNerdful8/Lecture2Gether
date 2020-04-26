<template>
    <v-container class="searchbar-cover"
                 :class="collapsed ? 'searchbar-cover-collapsed' : 'searchbar-cover-extended'">
        <v-card
            class="searchbar-background"
            color="primary"
            flat
            bottom
            >
                <h1 v-if="!collapsed" class="lecture2gether-heading display-4">Lecture&#x200b;2Gether</h1>
        </v-card>
        <v-form @submit.prevent="onWatch">
            <v-card :class="collapsed ? 'searchbar-collapsed' : 'searchbar-extended'"
                    class="mx-auto searchbar">
                <v-toolbar>
                    <v-text-field class="mx-auto" v-model="url" solo flat single-line hide-details label="Enter URL">
                    </v-text-field>
                    <v-btn depressed large type="submit">
                        Watch!
                    </v-btn>
                </v-toolbar>
            </v-card>
        </v-form>
    </v-container>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import { Watch, Prop } from 'vue-property-decorator';
import { Store } from 'vuex';
import { AuthState } from '@/plugins/store/player';


@Component({})
export default class Toolbar extends Vue {
    @Prop({ type: Boolean, default: false, required: false }) collapsed!: boolean

    url = '';

    // Called when the watch button is pressed.
    // The url variable contains the url from the text field at this point.
    @Watch('$store.state.player.password')
    async onWatch() {
        async function getL2goPlaylist(store: Store<any>, url: string, pass = '') {
            const apiUrl = `${store.state.settings.apiRoot}l2go`;
            return fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    // eslint-disable-next-line @typescript-eslint/camelcase
                    video_url: url,
                    password: pass,
                }),
            }).then((response) => {
                switch (response.status) {
                case 200:
                    store.commit('setAuthState', AuthState.UNNECESSARY);
                    return response.json();
                case 401:
                    store.commit(
                        'setAuthState',
                        pass === '' ? AuthState.NECESSARY : AuthState.FAILURE,
                    );
                    return '';
                case 403:
                    store.commit(
                        'setAuthState',
                        AuthState.FAILURE,
                    );
                    return '';
                default:
                    console.log(`${response.status}: Unexpected return code from l2go endpoint`);
                    return '';
                }
            }).catch((response) => {
                console.log(response);
                throw new Error(`${response.status}: Resource not available`);
            });
        }
        // update the url to point to the lecture2go playlist when it is a
        // lecture2go url
        let url: string = this.url;
        if (url.includes('lecture2go') || url.includes('/l2go/')) {
            const password = this.$store.state.player.password;
            url = await getL2goPlaylist(this.$store, url, password);
        }
        if (this.$store.state.isConnected && url !== '') this.$store.dispatch('setUrl', url);
        else console.warn('Not setting url because we are not connected');
    }
}
</script>

<style scoped lang="scss">
    .searchbar-cover {
        margin: 0;
        padding: 0;
        position: relative;
        top: 0;
        left: 0;
        width: 100%;
        max-width: 100%;
        transition: all 0.8s ease;
        margin-bottom: 64px;
    }

    .searchbar-cover-collapsed {
        height: 80px;
    }

    .searchbar-cover-extended {
        height: 50vh;
    }

    .searchbar-collapsed {
        transform: translateY(-72px);
    }

    .searchbar-extended {
        transform: translateY(-50%);
    }

    .searchbar-background {
        display: flex;
        align-items: flex-end;
        flex-direction: column;
        height: 100% !important;
        border-radius: 0 !important;
    }

    .searchbar {
        max-width: 700px;
        transition: all 0.8s ease;
    }

    .lecture2gether-heading {
        color: white;
        margin: auto;
        transition: all 0.8s ease;
        padding-left: 32px;
        padding-right: 32px;
    }
</style>
