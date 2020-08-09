import {Vue} from "vue/types/vue";

export{}

declare global {
    interface Document {
        application: Vue;

        test: string;
    }
}
