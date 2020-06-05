<template>
    <div class="title">
        {{ videoMetaData.Title }}
    </div>
</template>

<script lang="ts">
// eslint-disable-next-line import/no-extraneous-dependencies
import Component from 'vue-class-component';
import Vue from 'vue';
import { Watch } from 'vue-property-decorator';

@Component({
    components: { VideoMetaData },
})
export default class VideoMetaData extends Vue {

    get videoMetaData() {
        return this.$store.state.player.videoMetaData;
    }
}
</script>

<style scoped lang="scss">
</style>
