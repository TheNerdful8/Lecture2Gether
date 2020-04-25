<template>
    <v-container>
        <v-toolbar color="primary" dark prominent flat>
        </v-toolbar>
        <v-card class="mx-auto" max-width="1000" style="margin-top: -64px;">
            <v-toolbar flat>
                <v-text-field class="mx-auto" flat solo dense single-line hide-details label="Enter URL">
                </v-text-field>
                <v-spacer></v-spacer>
                <v-btn icon>
                    <v-icon>mdi-magnify</v-icon>
                </v-btn>
            </v-toolbar>
        </v-card>
    </v-container>
</template>

<script>
import Vue from 'vue';
import Component from 'vue-class-component';

@Component({})
export default class Toolbar extends Component {
}
</script>

<style scoped>

</style>
