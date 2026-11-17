"""
identity.py - persistent person identity on top of tracker IDs.

Problem: YOLO track IDs are temporary. When a person leaves the frame
and comes back, the tracker gives a NEW track ID.

Fix: keep a separate, permanent "person_id" decided by the FACE:
    track_id (temporary)  -->  person_id (permanent)

  * Known person   -> person_id = their name              ("Suyog")
  * Unknown person -> person_id = "Unknown_001", "Unknown_002", ...
    (their face encodings are stored, so the same unknown face gets the
     same ID next time, even after a restart)
"""

import os
import pickle
import time

import numpy as np


class IdentityManager:
    def __init__(
        self,
        known_names=None,
        known_encodings=None,
        known_tolerance=0.50,      # lower = stricter (face_recognition default is 0.6)
        unknown_tolerance=0.50,    # keep strict, otherwise different people get merged
        max_encodings_per_person=10,
        min_new_encoding_gap=0.25,  # only store an encoding if it adds a new "angle"
        store_path="unknown_gallery.pkl",
    ):
        self.known_tolerance = known_tolerance
        self.unknown_tolerance = unknown_tolerance
        self.max_enc = max_encodings_per_person
        self.min_gap = min_new_encoding_gap
        self.store_path = store_path

        self.known = {}      # name -> [encodings]
        self.unknown = {}    # "Unknown_001" -> {"encodings": [...], "first_seen": t, "last_seen": t}
        self.track_map = {}  # track_id -> person_id  (cache for live tracks)
        self._next_unknown = 1

        self.set_known(known_names or [], known_encodings or [])
        self._load()

    #  known
    def set_known(self, names, encodings):
        """(Re)load registered people. Call again any time to hot-reload."""
        known = {}
        for name, enc in zip(names, encodings):
            known.setdefault(name, []).append(np.asarray(enc))
        self.known = known

    #  tracking
    def get_identity(self, track_id):
        """Return person_id if this track was already identified, else None."""
        return self.track_map.get(track_id)

    def resolve(self, track_id, face_encoding):
        """
        Call when you have a face encoding for a track.
        Returns (person_id, is_known, is_new_person).
        """
        face_encoding = np.asarray(face_encoding)

        # 1) registered people
        name, dist = self._best_match(self.known, face_encoding)
        if name is not None and dist <= self.known_tolerance:
            self.track_map[track_id] = name
            return name, True, False

        # 2) unknown people we have already seen before
        uid, dist = self._best_match(
            {k: v["encodings"] for k, v in self.unknown.items()}, face_encoding
        )
        if uid is not None and dist <= self.unknown_tolerance:
            self._touch_unknown(uid, face_encoding)
            self.track_map[track_id] = uid
            return uid, False, False

        # 3) brand new unknown person
        uid = f"Unknown_{self._next_unknown:03d}"
        self._next_unknown += 1
        now = time.time()
        self.unknown[uid] = {
            "encodings": [face_encoding],
            "first_seen": now,
            "last_seen": now,
        }
        self.track_map[track_id] = uid
        self._save()
        return uid, False, True

    def forget_track(self, track_id):
        """Call for tracks that are gone, to keep the cache small."""
        self.track_map.pop(track_id, None)

    #  promote
    def promote(self, unknown_id, name):
        """
        Turn 'Unknown_007' into a named person once you know who it is.
        Returns the encodings so you can also save a face image to known_faces/.
        """
        data = self.unknown.pop(unknown_id, None)
        if data is None:
            return []
        self.known.setdefault(name, []).extend(data["encodings"])
        for t, p in list(self.track_map.items()):
            if p == unknown_id:
                self.track_map[t] = name
        self._save()
        return data["encodings"]

    #  helpers
    @staticmethod
    def _best_match(gallery, enc):
        best_id, best_dist = None, 1e9
        for pid, encs in gallery.items():
            if not encs:
                continue
            d = np.linalg.norm(np.asarray(encs) - enc, axis=1).min()
            if d < best_dist:
                best_id, best_dist = pid, d
        return best_id, best_dist

    def _touch_unknown(self, uid, enc):
        rec = self.unknown[uid]
        rec["last_seen"] = time.time()
        encs = rec["encodings"]
        # add the new view only if it's different enough from what we have
        if len(encs) < self.max_enc:
            if np.linalg.norm(np.asarray(encs) - enc, axis=1).min() > self.min_gap:
                encs.append(enc)
                self._save()

    #  persistence
    def _save(self):
        tmp = self.store_path + ".tmp"
        with open(tmp, "wb") as f:
            pickle.dump({"unknown": self.unknown, "next": self._next_unknown}, f)
        os.replace(tmp, self.store_path)  # atomic: no corrupt file if app crashes

    def _load(self):
        if not os.path.exists(self.store_path):
            return
        try:
            with open(self.store_path, "rb") as f:
                data = pickle.load(f)
            self.unknown = data["unknown"]
            self._next_unknown = data["next"]
        except Exception as e:  # corrupt file -> start fresh, don't crash
            print(f"[identity] could not load {self.store_path}: {e}")