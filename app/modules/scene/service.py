from modules.project.repository import ProjectRepository
from modules.scene.repository import SceneRepository
from modules.story.processor import AnimeStyle, StoryProcessing
from core.response import ApiResponse
from modules.scene.schemas import SceneResponse

class SceneService:
    def __init__(self):
        self.project_repo = ProjectRepository()
        self.scene_repo = SceneRepository()

    def segment_story(self, project_id: int, user_id: int) -> ApiResponse:
        try:
            project = self.project_repo.get_by_id(project_id, user_id)

            processor = StoryProcessing(
                target_duration=project.duration_sec,
                max_scenes=5,
                anime_style=AnimeStyle.SHONEN,
            )

            scenes_data = processor.process_story(project.story_text)
            db_scenes = self.scene_repo.create_many(scenes_data, project.id)
            response_data = [
                SceneResponse.model_validate(s).model_dump() for s in db_scenes
            ]

            return ApiResponse(
                message="Story segmented into scenes",
                status_code=200,
                data=response_data,
            )
        except Exception as e:
            return ApiResponse.error(message=str(e), status_code=500)
