import { ComponentBase, ComponentState } from "./componentBase";
import { ComponentId } from "../dataModels";

export type HighLevelComponentState = ComponentState & {
    _type_: "HighLevelComponent-builtin";
    _child_?: ComponentId;
};

export class HighLevelComponent extends ComponentBase {
    declare state: Required<HighLevelComponentState>;

    createElement(): HTMLElement {
        let element = document.createElement("div");
        element.classList.add("rio-high-level-component");
        return element;
    }

    updateElement(
        deltaState: HighLevelComponentState,
        latentComponents: Set<ComponentBase>
    ): void {
        super.updateElement(deltaState, latentComponents);

        this.replaceOnlyChild(latentComponents, deltaState._child_);
    }
}
