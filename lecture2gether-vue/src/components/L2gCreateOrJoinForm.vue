<template>
    <v-form>
        <v-text-field v-model="sessionId" label="Session ID"/>
        <v-btn v-if="sessionId !== ''" color="primary">Join</v-btn>
        <v-btn v-else color="primary">Create</v-btn>
    </v-form>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import 'vue-class-component/hooks';

@Component({})
export default class L2gCreateOrJoinForm extends Vue {
    public sessionId = '';
}
</script>

<style scoped lang="scss">

</style>
