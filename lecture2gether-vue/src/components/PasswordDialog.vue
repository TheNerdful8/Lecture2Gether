<template>
    <v-container>
        <v-card class="password-dialog pa-12">
            <v-container>
                <h2 class="display-3">
                    Video is password protected!
                </h2>
                <v-form @submit.prevent="sendPassword" class="ma-12">
                    <v-layout row justify-space-between>
                        <v-flex md9 class="d-flex align-center">
                            <v-text-field v-model="password" label="Password" type="password"></v-text-field>
                        </v-flex>
                        <v-flex md2 class="d-flex align-center">
                            <v-btn type="submit" color="secondary" class="password-button">Submit</v-btn>
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

    @Component({})
    export default class PasswordDialog extends Vue {
        password='';

        sendPassword() {
            // TODO
        }
    }
</script>

<style scoped lang="scss">
    .password-dialog {
        width: 853px;
        height: 480px;
    }
    .password-button {
    }
</style>
