<template>
    <v-container class="searchbar-cover">
        <v-toolbar :class="collapsed ? 'searchbar-background-collapsed' : 'searchbar-background-extended'" 
            color="primary" 
            flat>
        </v-toolbar>
        <v-card :class="collapsed ? 'searchbar-collapsed' : 'searchbar-extended'"
            class="mx-auto searchbar">
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

<script lang="ts">
import Vue, { PropType } from 'vue';
import Component from 'vue-class-component';
import { Prop } from 'vue-property-decorator';

@Component({})
export default class Toolbar extends Component {
    @Prop({type: Boolean, default: true, required: false}) collapsed: boolean
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

    .searchbar-background-collapsed {
        height: 80px!important;
    }

    .searchbar-background-extended {
        height: 100%!important;
    }

    .searchbar-collapsed {
        transform: translateY(-112%);
    }

    .searchbar-extended {
        transform: translateY(-50%);
    }

    .searchbar {
        max-width: 700px;
    }
</style>
