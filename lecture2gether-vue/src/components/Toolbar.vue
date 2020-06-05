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
                <div v-if="collapsed" style="position: absolute; top: 50%; transform:translateY(-50%); right:2em; color: #fff">
                    <v-icon dark class="mb-1 mr-1">mdi-account-group</v-icon>
                    {{userCount}}
                </div>
        </v-card>
        <v-form @submit.prevent="onWatch">
            <v-card :class="collapsed ? 'searchbar-collapsed' : 'searchbar-extended'"
                    class="mx-auto searchbar">
                <v-toolbar>
                    <v-text-field autofocus class="mx-auto" v-model="url" single-line hide-details label="Enter URL"
                                  :error="!urlIsValid">
                    </v-text-field>
                    <v-btn depressed large class="ml-4" color="secondary" type="submit">
                        Watch!
                    </v-btn>
                    <v-tooltip bottom v-model="showingTooltip">
                        <template v-slot:activator="_">
                            <v-btn @click="saveUrlClipboard()" class="canCopy share ml-4" color="primary" depressed outlined large type="button">
                                <v-icon>mdi-share</v-icon>
                            </v-btn>
                        </template>
                        <span>Copied share link</span>
                    </v-tooltip>
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
import { checkURL } from '@/mediaURLs';
import { VideoMetaDataWithUrl } from '@/api';


@Component({})
export default class Toolbar extends Vue {
    @Prop({ type: Boolean, default: false, required: false }) collapsed!: boolean

    url = '';

    showingTooltip = false;

    urlIsValid = true;

    // Called when the watch button is pressed.
    // The url variable contains the url from the text field at this point.
    @Watch('$store.state.player.password')
    async onWatch() {
        async function getVideoMetaData(store: Store<any>, url: string, pass = ''): Promise<VideoMetaDataWithUrl> {
            const apiUrl = `${store.state.settings.apiRoot}metadata`;
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
                default:
                    console.warn(`${response.status}: Unexpected return code from l2go endpoint`);
                    return '';
                }
            }).catch((response) => {
                console.debug(response);
                throw new Error(`${response.status}: Resource not available`);
            });
        }
        let url;
        try {
            url = new URL(this.url);
        } catch (e) {
            this.urlIsValid = false;
            return;
        }
        if (checkURL(url)) {
            const password = this.$store.state.player.password;
            const videoMetaData = await getVideoMetaData(this.$store, this.url, password);
            if (!videoMetaData) {
                this.urlIsValid = false;
            } else {
                this.urlIsValid = true;
                this.$store.dispatch('setUrl', videoMetaData.streamUrl);
                delete videoMetaData.streamUrl;
                this.$store.dispatch('setVideoMetaData', videoMetaData);
            }
        } else if (url.host === window.location.host) {
            // A lecture2gether url was entered, redirect to that room
            await this.$store.dispatch('leaveRoom');
            await this.$router.push(url.pathname);
        } else {
            this.urlIsValid = false;
        }
    }

    get userCount(): number {
        return this.$store.state.rooms.userCount;
    }

    // Save url to clipboard
    async saveUrlClipboard() {
        this.showingTooltip = true;
        const data = `${window.location.protocol}//${window.location.host}${this.$route.path}`;
        console.debug('Saved to clipboard: ', data);
        await navigator.clipboard.writeText(data);
        setTimeout(() => this.showingTooltip = false, 1000);
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
        margin-bottom: 128px;
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
