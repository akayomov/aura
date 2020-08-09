<template>
	<div class="field" :class="design?'design-'+design:''">
		<i v-if="icon!==''" :class="'gg-'+icon"/>
		<input :placeholder="placeholder" :value="currentValue" :readonly="!isEditing" :disabled="!isEditing" @change="handleChange"/>
	</div>
</template>

<script lang="ts">
import {Component, Emit, Prop, Vue, Watch} from 'vue-property-decorator'

@Component
export default class Field extends Vue {
	@Prop({default:""}) readonly icon!: string;
	@Prop({default:""}) readonly placeholder!: string;
	@Prop({default:""}) readonly design!: string;
	@Prop({default:""}) readonly value!: string;

	@Prop({default:true}) readonly editing!: boolean;
	isEditing: boolean = this.editing
	@Watch('editing',{immediate: true, deep: true})
	onEditing(val: boolean|string) {
		if(val === 'true') { this.isEditing = true }
		else if(val === 'false') {this.isEditing = false}
		else {
			//@ts-ignore
			this.isEditing = val
		}
	}

	@Watch('value')
	onValueChange(val: string) { this.currentValue = val }

	currentValue: string = this.value;
	@Emit('update')
	handleChange(e:Event) {
		//@ts-ignore
		this.currentValue = e.target.value
		return this.currentValue
	}
}
</script>

<style scoped lang="less">
@import "../tools/colors";

div.field {
	display: flex;
	flex-direction: row;
	align-items: center;
	i { margin-right: 5px; }
	input {
		font-family: 'default', serif;
		font-size: inherit;
		background: none;
		border: none;
		border-bottom: 2px solid @knob-back-default-inactive;
		padding-bottom: 3px;
		color: @main-foreground;
		flex-grow: 1;
		&:focus {
			outline-offset: 2px;
			outline: @component-focus-outline dashed 1px;
			border-bottom-color: @knob-back-default-active;
		}
		&::placeholder { color: @knob-back-default-hover }

		&[readonly] {
			border-bottom: none;
			user-select: none;
			tab-index: -1;
		}
	}
}
</style>