"""Print geom pairs when new contacts appear while closing the gripper."""

from pathlib import Path

import mujoco


MODEL_PATH = Path(__file__).parents[1] / "models" / "gripper.xml"


def geom_name(model: mujoco.MjModel, geom_id: int) -> str:
    name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, geom_id)
    return name or f"geom_{geom_id}"


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)
    seen_contacts: set[tuple[str, str]] = set()

    while data.time < 3.0:
        close_ratio = min(max((data.time - 0.5) / 1.5, 0.0), 1.0)
        data.ctrl[1:3] = 0.045 * close_ratio
        mujoco.mj_step(model, data)

        for contact_index in range(data.ncon):
            contact = data.contact[contact_index]
            pair = tuple(
                sorted(
                    (
                        geom_name(model, contact.geom1),
                        geom_name(model, contact.geom2),
                    )
                )
            )
            if pair not in seen_contacts:
                seen_contacts.add(pair)
                print(f"time={data.time:.3f}s new contact: {pair[0]} <-> {pair[1]}")

    print(f"unique contact pairs={len(seen_contacts)}")


if __name__ == "__main__":
    main()
