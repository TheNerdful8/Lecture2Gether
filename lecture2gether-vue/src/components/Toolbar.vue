<template>
    <v-container class="searchbar-cover">
        <v-toolbar class="searchbar-background" color="primary" prominent flat>
        </v-toolbar>
        <v-card class="searchbar mx-auto">
            <v-toolbar>
                <v-text-field class="mx-auto" solo flat single-line hide-details label="Enter URL">
                </v-text-field>
                <v-btn depressed large>
                    Watch!
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
    .searchbar-cover {
        margin: 0;
        padding: 0;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        max-width: 100%;
        height: 50vh;
    }

    .searchbar-background {
        margin: 0;
        height: 100%;
        max-height: 100%;
    }

    .searchbar {
        max-width: 700px;
        transform: translateY(-50%);
    }
</style>
