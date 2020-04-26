<template>
    <v-container>
        <v-card class="password-dialog pa-12">
            <v-container>
                <h2 class="display-3">
                    Video is password protected!
                </h2>
                <v-form @submit.prevent="sendPassword" class="ma-12" v-model="valid">
                    <v-layout row justify-space-between>
                        <v-flex md9 class="d-flex align-center">
                            <v-text-field v-model="password" label="Password" type="password"
                                          :rules="[rules.required]"></v-text-field>
                        </v-flex>
                        <v-flex md2 class="d-flex align-center">
                            <v-btn type="submit" color="secondary" class="password-button" :disabled="!valid">
                                <span v-if="!loading">Submit</span>
                                <span v-if="loading">
                                    <v-progress-circular color="white" indeterminate="true" size="24" width="3">
                                    </v-progress-circular>
                                </span>
                            </v-btn>
                        </v-flex>
                    </v-layout>
                </v-form>
            </v-container>
        </v-card>
    </v-container>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import { AuthState } from '@/plugins/store/player';

    @Component({})
export default class PasswordDialog extends Vue {
        password = '';

        valid = false;

        rules = {
            required: (value: string): boolean | string => !!value || 'Required.',
        }

        get authState() {
            return this.$store.state.player.auth;
        }

        get loading() {
            return this.authState === AuthState.CHECKING;
        }

        sendPassword() {
            this.$store.commit('setAuthState', AuthState.CHECKING);
            this.$store.commit('setPassword', this.password);
        }
}
</script>

<style scoped lang="scss">
    .password-dialog {
        width: 853px;
        height: 480px;
    }
    .password-button {
        width: 96px;
    }
</style>
