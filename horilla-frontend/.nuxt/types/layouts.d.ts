import blank from "/Users/omondiochieng/Repos/horilla-talent/horilla-frontend/layouts/blank.vue";
import _default from "/Users/omondiochieng/Repos/horilla-talent/horilla-frontend/layouts/default.vue";
import type { ComputedRef, MaybeRef } from 'vue'
declare module 'nuxt/app' {
  interface NuxtLayouts {
    'blank': InstanceType<typeof blank>['$props'],
    'default': InstanceType<typeof _default>['$props'],
}
  export type LayoutKey = keyof NuxtLayouts extends never ? string : keyof NuxtLayouts
  interface PageMeta {
    layout?: MaybeRef<LayoutKey | false> | ComputedRef<LayoutKey | false>
  }
}