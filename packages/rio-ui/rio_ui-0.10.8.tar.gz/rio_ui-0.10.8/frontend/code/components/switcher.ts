import { ComponentId } from "../dataModels";
import { ComponentBase, ComponentState } from "./componentBase";
import { componentsById } from "../componentManagement";
import { commitCss } from "../utils";

export type SwitcherState = ComponentState & {
    _type_: "Switcher-builtin";
    content?: ComponentId | null;
    transition_time?: number;
};

export class SwitcherComponent extends ComponentBase {
    declare state: Required<SwitcherState>;

    private activeChildContainer: HTMLElement | null = null;
    private resizerElement: HTMLElement | null = null;
    private idOfCurrentAnimation: number = 0;
    private isInitialized: boolean = false;

    createElement(): HTMLElement {
        let element = document.createElement("div");
        element.classList.add("rio-switcher");
        return element;
    }

    updateElement(
        deltaState: SwitcherState,
        latentComponents: Set<ComponentBase>
    ): void {
        super.updateElement(deltaState, latentComponents);

        // Update the transition time first, in case the code below is about
        // to start an animation.
        if (deltaState.transition_time !== undefined) {
            this.element.style.setProperty(
                "--rio-switcher-transition-time",
                `${deltaState.transition_time}s`
            );
        }

        // Update the child
        if (deltaState.content !== undefined) {
            if (!this.isInitialized) {
                if (deltaState.content !== null) {
                    // If this is the first time the switcher is being updated,
                    // don't animate anything.
                    this.activeChildContainer = document.createElement("div");
                    this.activeChildContainer.classList.add(
                        "rio-switcher-active-child"
                    );
                    this.element.appendChild(this.activeChildContainer);

                    this.replaceOnlyChild(
                        latentComponents,
                        deltaState.content,
                        this.activeChildContainer
                    );
                }
            } else if (deltaState.content !== this.state.content) {
                this.replaceContent(
                    deltaState.content,
                    latentComponents,
                    deltaState.transition_time ?? this.state.transition_time
                );
            }
        }

        this.isInitialized = true;
    }

    private async replaceContent(
        content: ComponentId | null,
        latentComponents: Set<ComponentBase>,
        transitionTime: number
    ): Promise<void> {
        // Animating the size is trickier than you might expect. Firstly, CSS
        // can't animate `width` and `height`, and secondly, our parent
        // component might force us to be larger than we want to be.
        //
        // The solution is create a child element and animate its min-size from
        // the size of the current child component to the size of the new child
        // component. (The other children will be made `absolute` during the
        // animation so they don't influence the Switcher's size.)

        // Step 1: Get the size of the current child element
        let oldChildContainer = this.activeChildContainer;
        let oldWidth: number = 0,
            oldHeight: number = 0;

        if (oldChildContainer !== null) {
            oldWidth = oldChildContainer.scrollWidth;
            oldHeight = oldChildContainer.scrollHeight;

            // The old component may be used somewhere else in the UI, so the
            // switcher can't rely on it still being available. To get around this,
            // create a copy of the element's HTML tree and use that for the
            // animation.
            //
            // Moreover, the component may have already been removed from the
            // switcher. This can happen when it was moved into another component.
            // Thus, fetch the component by its id, rather than using the contained
            // HTML node.
            let oldComponent = componentsById[this.state.content!]!;
            let oldElementClone = oldComponent.outerElement.cloneNode(
                true
            ) as HTMLElement;

            // Unparent the old component
            this.replaceOnlyChild(latentComponents, null, oldChildContainer);

            // Fill the childContainer with the cloned element
            oldChildContainer.appendChild(oldElementClone);

            oldChildContainer.classList.remove("rio-switcher-active-child");
        }

        // Step 2: Get the size of the new child component
        let newChildContainer: HTMLElement | null = null;
        let newWidth: number = 0,
            newHeight: number = 0;

        if (content !== null) {
            // Add the child into a helper container
            newChildContainer = document.createElement("div");
            this.replaceOnlyChild(latentComponents, content, newChildContainer);

            // Make it `absolute` so it isn't influenced by the Switcher's
            // current size
            newChildContainer.style.position = "absolute";
            newChildContainer.style.width = "min-content";
            this.element.appendChild(newChildContainer);

            // The child component's `updateElement` may not have run yet, which
            // would result in a size of 0x0. Wait a bit before we query its
            // size.
            [newWidth, newHeight] = await new Promise((resolve) => {
                requestAnimationFrame(() => {
                    resolve([
                        newChildContainer!.scrollWidth,
                        newChildContainer!.scrollHeight,
                    ]);
                });
            });

            newChildContainer.style.removeProperty("position");
            newChildContainer.style.removeProperty("width");

            commitCss(newChildContainer);

            newChildContainer.classList.add("rio-switcher-active-child");
        }
        this.activeChildContainer = newChildContainer;

        // Step 3: Animate the size of the invisible child element. If we're
        // currently still in the middle of an animation, re-use the existing
        // element and simply update its target size.
        let resizerElement: HTMLElement;

        if (this.resizerElement === null) {
            resizerElement = document.createElement("div");
            resizerElement.classList.add("rio-switcher-resizer");

            this.resizerElement = resizerElement;

            resizerElement.style.minWidth = `${oldWidth}px`;
            resizerElement.style.minHeight = `${oldHeight}px`;
            this.element.appendChild(resizerElement);

            this.element.classList.add("resizing");

            commitCss(resizerElement);
        } else {
            resizerElement = this.resizerElement;
        }

        resizerElement.style.minWidth = `${newWidth}px`;
        resizerElement.style.minHeight = `${newHeight}px`;

        // Step 4: Clean up
        this.idOfCurrentAnimation++;
        let idOfCurrentAnimation = this.idOfCurrentAnimation;

        // Clean up once the animation is finished
        setTimeout(() => {
            if (oldChildContainer !== null) {
                oldChildContainer.remove();
            }

            // If another animation was started before this one finished, we
            // don't need to do anything else.
            if (this.idOfCurrentAnimation !== idOfCurrentAnimation) {
                return;
            }

            resizerElement.remove();
            this.resizerElement = null;

            this.element.classList.remove("resizing");
        }, transitionTime * 1000);
    }
}
