<template>
    <div class="video-meta-data pa-6">
        <div class="video-title display-1"
             :class="{ hidden: videoMetaData.title === null }"
        >
            {{ videoMetaData.title }}
        </div>
        <div>
            <a class="creator body-1 meta-data-link"
               :href="videoMetaData.creatorLink"
               :class="{ hidden: videoMetaData.creator === null }"
            >
                {{ videoMetaData.creator }}
            </a>
            <div class="date body-1"
                 :class="{ hidden: videoMetaData.date === null }"
            >
                {{ videoDate }}
            </div>
        </div>
        <v-spacer></v-spacer>
        <a class="license body-1 meta-data-link"
           :href="videoMetaData.licenseLink"
           :class="{ hidden: videoMetaData.license === null }"
        >
            License: {{ videoMetaData.license }}
        </a>
    </div>
</template>

<script lang="ts">
// eslint-disable-next-line import/no-extraneous-dependencies
import Component from 'vue-class-component';
import Vue from 'vue';

@Component
export default class VideoMetaData extends Vue {
    get videoMetaData() {
        return this.$store.state.player.videoMetaData;
    }

    get videoDate() {
        const date = new Date(Date.parse(this.$store.state.player.videoMetaData.date));
        return date.toLocaleDateString();
    }
}
</script>

<style scoped lang="scss">
    .video-meta-data {
        text-align: left;
        display: grid;
        grid-gap: 1em;
        grid-template-columns: auto 1fr auto;
    }

    .video-title {
        grid-column: span 3;
    }

    .meta-data-link {
        color: #222222 !important;
    }

    .meta-data-link:link {
        text-decoration: none;
    }

    .meta-data-link:hover {
        text-decoration: underline;
    }

    .hidden {
        visibility: hidden;
    }
</style>
