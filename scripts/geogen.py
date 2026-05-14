import os


def generate_geckolib_item_model_class(name: str):
    # PascalCase class names
    class_base = ''.join(word.capitalize() for word in name.split('_'))
    class_name = f"{class_base}ItemModel"

    # Absolute path to your Java package directory
    base_dir = r"C:\Users\garat\Documents\cobblemon_fury_neoforge\src\main\java\com\lnc\cobblemonfury\item\model"
    file_path = os.path.join(base_dir, f"{class_name}.java")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure the folder exists

    # Java content
    content = f"""package com.lnc.cobblemonfury.item.model; 

import com.lnc.cobblemonfury.item.{class_base};
import net.minecraft.resources.ResourceLocation;
import software.bernie.geckolib.model.GeoModel;

public class {class_name} extends GeoModel<{class_base}> {{
    @Override
    public ResourceLocation getAnimationResource({class_base} animatable) {{
        return ResourceLocation.parse("cobblemonfury:animations/{name}.animation.json");
    }}

    @Override
    public ResourceLocation getModelResource({class_base} animatable) {{
        return ResourceLocation.parse("cobblemonfury:geo/{name}.geo.json");
    }}

    @Override
    public ResourceLocation getTextureResource({class_base} animatable) {{
        return ResourceLocation.parse("cobblemonfury:textures/item/{name}.png");
    }}
}}
"""

    # Write to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Java file generated at: {file_path}")
    

def generate_dynamic_gun_item_class(name: str):
    # Convert to PascalCase class name (e.g. dragon_gun → DragonGun)
    class_base = ''.join(word.capitalize() for word in name.split('_'))

    # Absolute target path
    file_path = rf"C:\Users\garat\Documents\cobblemon_fury_neoforge\src\main\java\com\lnc\cobblemonfury\item\{class_base}.java"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Java content (dynamic class name and model name)
    content = f"""package com.lnc.cobblemonfury.item;

import com.lnc.cobblemonfury.entity.weapons.ProjoElec;
import com.lnc.cobblemonfury.init.ModEntities;
import com.lnc.cobblemonfury.item.model.{class_base}ItemModel;
import com.lnc.cobblemonfury.procedures.utils.WeaponsUtils;
import net.minecraft.client.renderer.BlockEntityWithoutLevelRenderer;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.UseAnim;
import net.minecraft.world.level.Level;
import org.jetbrains.annotations.NotNull;
import software.bernie.geckolib.animatable.GeoItem;
import software.bernie.geckolib.animatable.SingletonGeoAnimatable;
import software.bernie.geckolib.animatable.client.GeoRenderProvider;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animatable.instance.SingletonAnimatableInstanceCache;
import software.bernie.geckolib.animation.AnimatableManager;
import software.bernie.geckolib.animation.AnimationController;
import software.bernie.geckolib.animation.PlayState;
import software.bernie.geckolib.animation.RawAnimation;
import software.bernie.geckolib.renderer.GeoItemRenderer;

import java.util.function.Consumer;

public class {class_base} extends Item implements GeoItem {{

    private static final WeaponsUtils w = new WeaponsUtils();
    private static final RawAnimation SHOOT_ANIM = RawAnimation.begin().thenPlay("animation.model.shoot");
    private static final RawAnimation RELEASE_ANIM = RawAnimation.begin().thenPlay("animation.model.release");

    private final AnimatableInstanceCache cache = new SingletonAnimatableInstanceCache(this);

    public {class_base}(Properties properties) {{
        super(properties.durability(400));
        SingletonGeoAnimatable.registerSyncedAnimatable(this);
    }}

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {{
        controllers.add(new AnimationController<>(this, "AnimationController", 0, state -> PlayState.STOP)
                .triggerableAnim("shoot", SHOOT_ANIM).triggerableAnim("release", RELEASE_ANIM));
    }}

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {{
        return cache;
    }}

    @Override
    public boolean shouldCauseReequipAnimation(ItemStack oldStack, ItemStack newStack, boolean slotChanged) {{
        return false;
    }}

    @Override
    public void createGeoRenderer(Consumer<GeoRenderProvider> consumer) {{
        consumer.accept(new GeoRenderProvider() {{
            private {class_base}ItemRenderer renderer;

            @Override
            public BlockEntityWithoutLevelRenderer getGeoItemRenderer() {{
                if (this.renderer == null)
                    this.renderer = new {class_base}ItemRenderer();
                return this.renderer;
            }}
        }});
    }}

    public class {class_base}ItemRenderer extends GeoItemRenderer<{class_base}> {{
        public {class_base}ItemRenderer() {{
            super(new {class_base}ItemModel());
        }}
    }}

    @Override
    public @NotNull UseAnim getUseAnimation(@NotNull ItemStack itemstack) {{
        return UseAnim.NONE;
    }}

    @Override
    public @NotNull InteractionResultHolder<ItemStack> use(@NotNull Level world, @NotNull Player player,
                                                           @NotNull InteractionHand hand) {{
        InteractionResultHolder<ItemStack> ar = super.use(world, player, hand);
        player.startUsingItem(hand); // Start using (charging) the item
        if ((player.getMainHandItem().getItem() instanceof {class_base}))
            if (world instanceof ServerLevel serverLevel) {{
                triggerAnim(player, GeoItem.getOrAssignId(player.getItemInHand(hand), serverLevel),
                        "AnimationController",
                        "shoot");
            }}
        w.weaponShoot(new ProjoElec(ModEntities.PROJO_ELEC.get(), world), player, world, 3, 2,
                ParticleTypes.ELECTRIC_SPARK, "entity.firework_rocket.blast", ar.getObject(), 1);
        return ar;
    }}
}}
"""

    # Write the Java file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Java file generated at: {file_path}")

import json

def convert_display_settings(name: str):
    input_path = os.path.join(os.path.dirname(__file__), f"{name}.json")

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Remove "textures"
    data.pop("textures", None)

    # Rebuild dict to insert "parent" after "credit"
    new_data = {}

    for key in data:
        new_data[key] = data[key]
        if key == "credit":
            new_data["parent"] = "builtin/entity"

    # If somehow "credit" is missing, just add parent at start
    if "credit" not in data:
        new_data = {"parent": "builtin/entity", **new_data}

    output_path = os.path.join(
        os.path.dirname(__file__),
        "C:\\Users\\garat\\Documents\\cobblemon_fury_neoforge\\src\\main\\resources\\assets\\cobblemonfury\\models\\displaysettings",
        f"{name}.item.json"
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2)

    print(f"✅ Converted and saved display settings: {output_path}")
    
import os
import shutil

def copy_geo_json(name: str):
    # Source file path (in same folder as this script)
    src_path = os.path.join(os.path.dirname(__file__), f"{name}.geo.json")

    # Destination file path (fixed folder, named dragon_gun.geo.json)
    dest_path = rf"C:\Users\garat\Documents\cobblemon_fury_neoforge\src\main\resources\assets\cobblemonfury\geo\{name}.geo.json"

    # Ensure destination folder exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Copy file
    shutil.copyfile(src_path, dest_path)

    print(f"✅ Geo JSON file copied to: {dest_path}")

# Example usage
# copy_geo_json("dragon_gun")

import os
import json

def create_item_model_json(name: str):
    data = {
        "parent": f"cobblemonfury:displaysettings/{name}.item",
        "textures": {
            "layer0": f"cobblemonfury:item/{name}"
        }
    }

    output_path = rf"C:\Users\garat\Documents\cobblemon_fury_neoforge\src\main\resources\assets\cobblemonfury\models\item\{name}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Item model JSON created at: {output_path}")

# Example usage
# create_item_model_json("dragon_gun")

import os
import shutil

def copy_animation_json(name: str):
    # Source file path in same folder as script
    src_path = os.path.join(os.path.dirname(__file__), f"{name}.animation.json")

    # Destination file path
    dest_path = rf"C:\Users\garat\Documents\cobblemon_fury_neoforge\src\main\resources\assets\cobblemonfury\animations\{name}.animation.json"

    # Ensure destination folder exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Copy file
    shutil.copyfile(src_path, dest_path)

    print(f"✅ Animation JSON copied to: {dest_path}")

# Example usage
# copy_animation_json("dragon_gun")

import os
import shutil

def copy_texture_png(name: str):
    # Source file path in same folder as script
    src_path = os.path.join(os.path.dirname(__file__), f"{name}.png")

    # Destination path
    dest_path = rf"C:\Users\garat\Documents\cobblemon_fury_neoforge\src\main\resources\assets\cobblemonfury\textures\item\{name}.png"

    # Ensure destination folder exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Copy the PNG file
    shutil.copyfile(src_path, dest_path)

    print(f"✅ Texture PNG copied to: {dest_path}")

# Example usage
# copy_texture_png("dragon_gun")


def generate_geo(name:str):
    generate_geckolib_item_model_class(name)
    generate_dynamic_gun_item_class(name)
    convert_display_settings(name)
    copy_geo_json(name)
    create_item_model_json(name)
    copy_animation_json(name)
    copy_texture_png(name)

# generate_geo("katana_fire")
# generate_geo("katana_poison")
# generate_geo("block_placer")
generate_geo("plant_gun")