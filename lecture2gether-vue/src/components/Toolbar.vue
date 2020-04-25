<template>
    <v-container class="searchbar-cover"
                 :class="collapsed ? 'searchbar-cover-collapsed' : 'searchbar-cover-extended'">
        <v-toolbar
            class="searchbar-background"
            color="primary"
            flat>
            <h1 v-if="!collapsed" class="lecture2gether-heading display-4">Lecture&#x200b;2Gether</h1>
        </v-toolbar>
        <v-card :class="collapsed ? 'searchbar-collapsed' : 'searchbar-extended'"
                class="mx-auto searchbar">
            <v-toolbar>
                <v-text-field class="mx-auto" v-model="url" solo flat single-line hide-details label="Enter URL">
                </v-text-field>
                <v-btn depressed large @click="watch()">
                    Watch!
                </v-btn>
            </v-toolbar>
        </v-card>
    </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from 'vue';
import Component from 'vue-class-component';
import { Prop } from 'vue-property-decorator';

@Component({})
export default class Toolbar extends Component {
    url = "";

    //Called when the watch button is pressed.
    //The url variable contains the url from the text field at this point.
    watch() {
        this.$store.dispatch("setUrl", this.url);
    };

    @Prop({type: Boolean, default: false, required: false}) collapsed: boolean
}
</script>

<style scoped lang="scss">
    .searchbar-cover {
        margin: 0;
        padding: 0;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        max-width: 100%;
        transition: all 0.8s ease;
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
        height: 100%!important;
    }

    .searchbar {
        max-width: 700px;
        transition: all 0.8s ease;
    }

    .lecture2gether-heading {
        color: white;
        margin: auto;
        padding-top: 64px;
        transition: all 0.8s ease;
    }
</style>
