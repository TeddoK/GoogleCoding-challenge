"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self,name):
        self.name = name
        self.videos=[]

    def add_video(self, video, playlist_name):
        videoExists= False
        flagged = False

        for existingVideo in self.videos:
            if existingVideo == video:
                videoExists = True
                print(f"Cannot add video to {playlist_name}: Video already added")

        if video.flags != []:
                    print(f"Cannot add video to {playlist_name}: Video is currently flagged {video.flags[0]}")
                    flagged = True

        if (not videoExists) and (not flagged):
            self.videos.append(video)
            print(f"Added video to {playlist_name}: {video.title}")

    def remove_video(self, video, playlist_name):
        videoExists= False

        for existingVideo in self.videos:
            if existingVideo == video:
                videoExists = True
                self.videos.remove(video)
                print(f"Removed video from {playlist_name}: {video.title}")

        if not videoExists:
            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")