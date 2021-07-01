"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.current_video = {"title" : "" , "paused" : False}
        self.current_playlists = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        
        videoList = []

        for video in self._video_library.get_all_videos():

            tagStr = ""
            for tag in video.tags:
                tagStr += tag + " "
            tagStr = tagStr[:-1]

            if video.flags == []:
                videoList.append(f"{video.title} ({video.video_id}) [{tagStr}]")

            else:
                videoList.append(f"{video.title} ({video.video_id}) [{tagStr}] - FLAGGED {video.flags[0]}")

        videoList.sort()

        print("Here's a list of all available videos:")

        for video in videoList:
            print (video)


    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """

        try:
            new_video = self._video_library.get_video(video_id)

            if new_video.flags == []:
                if self.current_video["title"] != "":
                    print(f"Stopping video: {self.current_video['title']}")

                self.current_video["title"] = new_video.title
                self.current_video["paused"] = False

                print(f"Playing video: {self.current_video['title']}")
            else:
                print(f"Cannot play video: Video is currently flagged {new_video.flags[0]}")

        except:
            print("Cannot play video: Video does not exist")


    def stop_video(self):
        """Stops the current video."""
        if self.current_video["title"] == "":
            print("Cannot stop video: No video is currently playing")

        else:
            print(f"Stopping video: {self.current_video['title']}")
            self.current_video["title"] = ""
            self.current_video["paused"] = False

    def play_random_video(self):
        """Plays a random video from the video library."""
        import random
        videoList = []

        for video in self._video_library.get_all_videos():
            if len(video.flags) <= 0:
                videoList.append(video.title)

        if self.current_video["title"] != "":
                print(f"Stopping video: {self.current_video['title']}")
        try:
            self.current_video["title"]= random.choice(videoList)
            self.current_video["paused"]= False

            print(f"Playing video: {self.current_video['title']}")
        except:
            print("No videos available")


    def pause_video(self):
        """Pauses the current video."""

        if self.current_video["title"] == "":
            print("Cannot pause video: No video is currently playing")

        elif self.current_video["paused"]:
            print(f"Video already paused: {self.current_video['title']}")

        else:
            self.current_video["paused"] = True
            print(f"Pausing video: {self.current_video['title']}")

    def continue_video(self):
        """Resumes playing the current video."""

        if self.current_video["title"] == "":
            print("Cannot continue video: No video is currently playing")

        elif not self.current_video["paused"]:
            print(f"Cannot continue video: Video is not paused")

        else:
            self.current_video["paused"] = False
            print(f"Continuing video: {self.current_video['title']}")

    def show_playing(self):
        """Displays video currently playing."""

        if self.current_video["title"] == "":
            print("No video is currently playing")

        else:

            for video in self._video_library.get_all_videos():
                
                if video.title == self.current_video["title"]:
                    
                    tagStr = ""
                    for tag in video.tags:
                        tagStr += tag + " "
                    tagStr = tagStr[:-1]

                    if self.current_video["paused"]:

                        print(f"Currently playing: {video.title} ({video.video_id}) [{tagStr}] - PAUSED")

                    else:

                        print(f"Currently playing: {video.title} ({video.video_id}) [{tagStr}]")
                    break

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        validName= True
        for char in playlist_name:
            if char == " ":
                print("You cannot have any whitespace in your playlist name")
                validName=False

        if validName:

            nameAlreadyUsed= False
            for playlist in self.current_playlists:
                if playlist_name.lower() == playlist:
                    nameAlreadyUsed = True
                    print("Cannot create playlist: A playlist with the same name already exists")

            if not nameAlreadyUsed:
                self.current_playlists[playlist_name.lower()]=Playlist(playlist_name)
                print(f"Successfully created new playlist: {playlist_name}")


    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        playlistExists= False
        videoExists = False
        for playlist in self.current_playlists:
            if playlist_name.lower() == playlist:

                playlistExists = True
                for video in self._video_library.get_all_videos():
                    if video_id == video.video_id:

                        videoExists=True
                        self.current_playlists[playlist].add_video(video, playlist_name)

        if not playlistExists:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")       

        elif not videoExists:
            print(f"Cannot add video to {playlist_name}: Video does not exist")

    def show_all_playlists(self):
        """Display all playlists."""
        if len(self.current_playlists) == 0:
            print("No playlists exist yet") 
        else:
            print("Showing all playlists:")
            playlists=[]

            for playlist in self.current_playlists:
                playlists.append(self.current_playlists[playlist].name)

            playlists=sorted(playlists, key= str.casefold)

            for playlist in playlists:
                print(f"  {playlist}")


    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlistExists = False
        for playlist in self.current_playlists:
            if playlist_name.lower() == playlist:
                playlistExists = True

                print(f"Showing playlist: {playlist_name}")
                if self.current_playlists[playlist].videos == []:
                    print("  No videos here yet")
                else:
                    videoList = []

                    for video in self.current_playlists[playlist].videos:

                        tagStr = ""
                        for tag in video.tags:
                            tagStr += tag + " "
                        tagStr = tagStr[:-1]

                        if video.flags == []:
                            print(f"  {video.title} ({video.video_id}) [{tagStr}]")

                        else:
                            print(f"{video.title} ({video.video_id}) [{tagStr}] - FLAGGED {video.flags[0]}")

        if not playlistExists:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")



    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlistExists= False
        videoExists = False
        for playlist in self.current_playlists:
            if playlist_name.lower() == playlist:

                playlistExists = True
                for video in self._video_library.get_all_videos():
                    if video_id == video.video_id:

                        videoExists=True
                        self.current_playlists[playlist].remove_video(video, playlist_name)

        if not playlistExists:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")       

        elif not videoExists:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlistExists = False
        for playlist in self.current_playlists:
            if playlist_name.lower() == playlist:
                playlistExists = True

                self.current_playlists[playlist].videos = []
                print(f"Successfully removed all videos from {playlist_name}")

        if not playlistExists:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlistExists = False
        for playlist in self.current_playlists:
            if playlist_name.lower() == playlist:
                playlistExists = True

                del self.current_playlists[playlist]
                print(f"Deleted playlist: {playlist_name}")
                break

        if not playlistExists:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videoList = []

        for video in self._video_library.get_all_videos():

            if video.title.lower().find(search_term.lower()) >= 0 and video.flags == []:
                videoList.append(video)

        if len(videoList) > 0:
            videoList.sort(key= lambda x: x.title)

            print(f"Here are the results for {search_term}:")

            for i in range(len(videoList)):

                tagStr = ""
                for tag in videoList[i].tags:
                    tagStr += tag + " "
                tagStr = tagStr[:-1]

                print (f"  {i+1}) {videoList[i].title} ({videoList[i].video_id}) [{tagStr}]")

            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")

            videoIndex = input("")
            try:   
                videoID = videoList[int(videoIndex)-1].video_id
                self.play_video(videoID)
            except:
                pass

        else:
            print(f"No search results for {search_term}")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """

